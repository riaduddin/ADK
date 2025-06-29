import os
import sys
import uuid
import shutil
import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from fastapi import BackgroundTasks

import vertexai
from vertexai.preview import reasoning_engines
from BOQ_development_agent.agent import root_agent

from pymongo import MongoClient

# from storing_data import get_component_from_db, store_component_in_db



# 1. Load and validate environment variables
load_dotenv()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
from pathlib import Path
print(f"Loaded .env from: {Path('.env').resolve()}")
print(f"GOOGLE_CLOUD_PROJECT={os.getenv('GOOGLE_CLOUD_PROJECT')}")


if not project_id or not location:
    print("Missing required environment variable: GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_LOCATION")
    sys.exit(1)
    
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)
db = client["engineering_components"]

def store_component_in_db(collection_name, component_data, user_id, session_id):
    collection = db[collection_name]
    if component_data:
        doc = {
            "user_id": user_id,
            "session_id": session_id,
            "data": component_data,
            "status": "completed"
        }
    else:
        doc = {
            "user_id": user_id,
            "session_id": session_id,
            "data": component_data,
            "status": "failed"
        }
    result = collection.insert_one(doc)
    print(f"📥 Stored in '{collection_name}' with _id: {result.inserted_id}")

def get_component_from_db(collection_name, user_id, session_id):
    collection = db[collection_name]
    result = collection.find_one({"user_id": user_id, "session_id": session_id})
    if result:
        return result.get("data", {})
    else:
        raise HTTPException(status_code=404, detail=f"{collection_name} not found for given user and session.")
    
    
def process_file_in_background(user_id: str, session_id: str, file_path: str):
    from storing_data import store_component_in_db
    import json
    import os

    boq_data = None
    validation_result = None
    validdation_count = 0

    try:
        app_stream = app_instance.stream_query(
            user_id=user_id,
            session_id=session_id,
            message=f"[FILE] {file_path}",
        )

        for event in app_stream:
            try:
                part_text = event["content"]["parts"][0]["text"]

                if part_text.startswith("```json"):
                    part_text = part_text.replace("```json", "").strip()
                if part_text.endswith("```"):
                    part_text = part_text[:-3].strip()

                print("✅ Cleaned JSON text:", part_text)

                parsed = json.loads(part_text)

                if "boq" in parsed:
                    boq_data = parsed["boq"]
                    print("📦 Captured BoQ data")

                if "validation" in parsed:
                    validdation_count+=1
                    validation_result = parsed
                    print("🧪 Captured validation result:", validation_result)

                    if validation_result.get("validation") == "pass" and boq_data:
                        store_component_in_db("boq", boq_data, user_id, session_id)
                        break
                    elif "validation" in parsed and validdation_count ==3:
                        print("❗️ Validation failed after 3 attempts, stopping stream.")
                        store_component_in_db("boq", boq_data, user_id, session_id)
                        break
                    continue
                for key in [
                    "component_geometry", "pile_details", "reinforcement_details",
                    "material_specs", "seismic_arrestors", "structural_notes", 
                    "compliance_parameters"
                ]:
                    if key in parsed:
                        store_component_in_db(key, parsed[key], user_id, session_id)

            except Exception as e:
                print(f"❌ Stream event processing failed: {e}")

    except Exception as e:
        print(f"❌ Background processing failed: {e}")

    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🧹 Deleted temporary file: {file_path}")
        except Exception as cleanup_err:
            print(f"⚠️ Failed to delete temp file: {cleanup_err}")


# 2. Initialize Vertex AI & ADK app
vertexai.init(project=project_id, location=location)
app_instance = reasoning_engines.AdkApp(agent=root_agent, enable_tracing=True)

# 3. Create FastAPI app
app = FastAPI(title="ADK + FastAPI Server")


# -- Data models -------------------------------------------------------------
class QueryInput(BaseModel):
    user_id: str
    session_id: str
    message: str


# -- Endpoints ---------------------------------------------------------------

@app.post("/create_session/")
async def create_session(user_id: str):
    """
    Create a new ADK session for the given user_id.
    """
    try:
        session = app_instance.create_session(user_id=user_id)
        return {
            "session_id": session.id,
            "user_id": session.user_id,
            "app_name": session.app_name,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list_sessions/")
async def list_sessions(user_id: str):
    """
    List all sessions for the given user_id.
    """
    try:
        sessions = app_instance.list_sessions(user_id=user_id)
        if hasattr(sessions, "sessions"):
            return {"sessions": sessions.sessions}
        elif hasattr(sessions, "session_ids"):
            return {"session_ids": sessions.session_ids}
        else:
            return {"raw": str(sessions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/")
async def stream_query(input: QueryInput):
    """
    Send a text message into an existing session and return the aggregated response.
    """
    try:
        response = ""
        for event in app_instance.stream_query(
            user_id=input.user_id,
            session_id=input.session_id,
            message=input.message,
        ):
            if hasattr(event, "text"):
                response += event.text
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/upload/")
async def upload_file(
    background_tasks: BackgroundTasks,
    user_id: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Upload a PDF and trigger background processing.
    Returns only the session_id immediately.
    """
    # Save file
    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(upload_dir, unique_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Create ADK session
    try:
        session = app_instance.create_session(user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {e}")

    # Kick off background task
    background_tasks.add_task(process_file_in_background, user_id, session.id, file_path)

    return {
        "status": "processing",
        "session_id": session.id,
    }

# @app.post("/upload/")
# async def upload_file(
#     user_id: str = Form(...),
#     file: UploadFile = File(...),
#     ):
#     """
#     Upload a PDF file and send it to the ADK agent as a [FILE] message.
#     Mimics the ADK Web UI behavior.
#     """
#     # 1. Save the file locally
#     print(f"Received file: {file.filename} (size: {file.size} bytes)")
#     upload_dir = "uploaded_files"
#     os.makedirs(upload_dir, exist_ok=True)
#     print(f"Upload directory: {upload_dir}")
#     unique_name = f"{uuid.uuid4()}_{file.filename}"
#     file_path = os.path.join(upload_dir, unique_name)

#     try:
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

#     # 2. Create a new session (you can also accept session_id if you prefer)
#     try:
#         session = app_instance.create_session(user_id=user_id)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to create session: {e}")

#     # 3. Send the “[FILE] /path/to/file.pdf” message
#     response_texts = []
#     merged_output = {}
#     boq_data=None
#     validation_result=None
#     try:
#         for event in app_instance.stream_query(
#             user_id=user_id,
#             session_id=session.id,
#             message=f"[FILE] {file_path}",
#         ):
#             try:
#                 part_text = event["content"]["parts"][0]["text"]

#                 if part_text.startswith("```json"):
#                     part_text = part_text.replace("```json", "").strip()
#                 if part_text.endswith("```"):
#                     part_text = part_text[:-3].strip()

#                 print("✅ Cleaned JSON text:", part_text)

#                 # if "validation" in part_text.lower():
#                 #     print("🔁 Found 'validation' — stopping stream")
#                 #     break

#                 response_texts.append(part_text)

#                 try:
#                     parsed = json.loads(part_text)
                    
#                     if "boq" in parsed:
#                         boq_data = parsed["boq"]
#                         print("📦 Captured BoQ data")
                        
#                     if "validation" in parsed:
#                         validation_result = parsed
#                         print("🧪 Captured validation result:", validation_result)

#                         # ✅ If validation is 'pass', add BoQ and exit loop early
#                         if validation_result.get("validation") == "pass" and boq_data:
#                             merged_output["boq"] = boq_data
#                             print("✅ BoQ passed validation — exiting stream early.")
#                             store_component_in_db("boq", boq_data, user_id, session.id)
#                             break
#                         continue
#                     for key in ["component_geometry","pile_details","reinforcement_details","material_specs","seismic_arrestors","structural_notes","compliance_parameters"]:
#                         if key in parsed:
#                             store_component_in_db(key, parsed[key], user_id, session.id)

#                     # Merge top-level keys without extracting nested parts
#                     if isinstance(parsed, list):
#                         for item in parsed:
#                             if isinstance(item, dict):
#                                 merged_output.update(item)
#                     elif isinstance(parsed, dict):
#                         merged_output.update(parsed)
                        
#                     #print("✅ Parsed JSON successfully:", merged_output)

#                 except json.JSONDecodeError as err:
#                     print("❌ Failed to parse JSON:", err)

#             except (KeyError, IndexError, TypeError) as e:
#                 print("❌ Could not extract text from event:", e)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Agent processing failed: {e}")

#     finally:
#         try:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#                 print(f"🧹 Deleted temporary file: {file_path}")
#         except Exception as cleanup_err:
#             print(f"⚠️ Failed to delete temp file: {cleanup_err}")
            
#     if validation_result.get("validation") == "fail" and boq_data:
#         store_component_in_db("boq", parsed["boq"], user_id, session.id)
            
#     return {
#         "status": "success",
#         "file_saved_as": unique_name,
#         "session_id": session.id,
#         "structured_outputs": merged_output
#     }



@app.get("/component_geometry")
async def get_component_geometry(user_id: str, session_id: str):
    return get_component_from_db("component_geometry", user_id, session_id)

@app.get("/pile_details")
async def get_pile_details(user_id: str, session_id: str):
    return get_component_from_db("pile_details", user_id, session_id)

@app.get("/reinforcement_details")
async def get_reinforcement_details(user_id: str, session_id: str):
    return get_component_from_db("reinforcement_details", user_id, session_id)

@app.get("/material_specs")
async def get_material_specs(user_id: str, session_id: str):
    return get_component_from_db("material_specs", user_id, session_id)

@app.get("/seismic_arrestors")
async def get_seismic_arrestors(user_id: str, session_id: str):
    return get_component_from_db("seismic_arrestors", user_id, session_id)

@app.get("/structural_notes")
async def get_structural_notes(user_id: str, session_id: str):
    return get_component_from_db("structural_notes", user_id, session_id)

@app.get("/compliance_parameters")
async def get_compliance_parameters(user_id: str, session_id: str):
    return get_component_from_db("compliance_parameters", user_id, session_id)

@app.get("/boq")
async def get_boq(user_id: str, session_id: str):
    return get_component_from_db("boq", user_id, session_id)

# -- Run with uvicorn -------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8060, reload=True)

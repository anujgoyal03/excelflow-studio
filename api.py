from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from engine import process_workbook, ProcessingError


app = FastAPI(
    title="ExcelFlow Enterprise Studio API",
    version="1.0.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/")
async def root():

    return {
        "success": True,
        "message": "ExcelFlow API is running"
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/api/health")
async def health_check():

    return {
        "success": True,
        "message": "ExcelFlow API is running"
    }


# ---------------------------------------------------------
# PROCESS EXCEL
# ---------------------------------------------------------

@app.post("/api/process")
async def process_excel(

    source_file: UploadFile = File(...),

    target_file: UploadFile = File(...),

    mode: str = Form("all")

):

    try:

        # -------------------------------------------------
        # Allowed modes
        # -------------------------------------------------

        allowed_modes = {
            "all",
            "pp",
            "task_attributes",
            "user_stories"
        }


        if mode not in allowed_modes:

            raise HTTPException(

                status_code=400,

                detail=(
                    f"Invalid mode: {mode}. "
                    f"Allowed modes: "
                    f"{', '.join(sorted(allowed_modes))}"
                )

            )


        # -------------------------------------------------
        # Read uploaded files
        # -------------------------------------------------

        source_bytes = await source_file.read()

        target_bytes = await target_file.read()


        # -------------------------------------------------
        # Validate files
        # -------------------------------------------------

        if not source_bytes:

            raise HTTPException(
                status_code=400,
                detail="Source Excel file is empty."
            )


        if not target_bytes:

            raise HTTPException(
                status_code=400,
                detail="Template Excel file is empty."
            )


        # -------------------------------------------------
        # Call your existing engine.py
        # -------------------------------------------------

        output_bytes, processed_sheets, log_lines = (
            process_workbook(
                source_bytes=source_bytes,
                target_bytes=target_bytes,
                mode=mode
            )
        )


        # -------------------------------------------------
        # Create output filename
        # -------------------------------------------------

        original_name = (
            target_file.filename
            or "Template.xlsx"
        )


        if original_name.lower().endswith(".xlsx"):

            output_filename = (
                original_name[:-5]
                + "_Processed.xlsx"
            )

        else:

            output_filename = (
                original_name
                + "_Processed.xlsx"
            )


        # -------------------------------------------------
        # Return processed Excel file
        # -------------------------------------------------

        return Response(

            content=output_bytes,

            media_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),

            headers={

                "Content-Disposition":
                    f'attachment; filename="{output_filename}"',

                "X-Processed-Sheets":
                    str(len(processed_sheets)),

                "X-Mode":
                    mode,

                "X-Status":
                    "success"

            }

        )


    # -----------------------------------------------------
    # Known processing errors
    # -----------------------------------------------------

    except ProcessingError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


    # -----------------------------------------------------
    # FastAPI errors
    # -----------------------------------------------------

    except HTTPException:

        raise


    # -----------------------------------------------------
    # Unexpected errors
    # -----------------------------------------------------

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"Unexpected error: {str(e)}"

        )
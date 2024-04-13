import io
from datetime import datetime
from typing import List

import pandas as pd
from loguru import logger
from pydantic import BaseModel
from starlette.responses import StreamingResponse


async def export_template(
    schema: BaseModel, file_name: str, data_list: List[BaseModel] = None
) -> StreamingResponse:
    """
    Export template or date
    """
    global excel_writer
    field_names = schema.__fields__
    user_export_df = pd.DataFrame(columns=field_names)
    if data_list is not None:
        data_dicts = [item.dict() for item in data_list]
        user_export_df = user_export_df._append(data_dicts, ignore_index=True)
    filename = f"{file_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    stream = io.BytesIO()
    try:
        excel_writer = pd.ExcelWriter(stream, engine="xlsxwriter")
        user_export_df.to_excel(excel_writer, index=False)
        excel_writer._save()
        stream.seek(0)
        return StreamingResponse(
            io.BytesIO(stream.getvalue()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logger.error(f"{e}")
    finally:
        excel_writer.close()

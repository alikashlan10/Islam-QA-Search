# import dependencies
from src.api.dependencies import retrieve_use_case
from src.logger.logger import setup_logger

logger = setup_logger(__name__)

# define query

query = "هل يجوز دفع مال للرشوة"

# execute usecase
results  = retrieve_use_case.execute(query = query , top_k =5 )

# log results
for res in results:
    logger.info(f"score : {res.score}")
    logger.info(f"title : {res.title}")
    logger.info(f"chunk : {res.chunk}")
    logger.info(f"video id : {res.video_id}")

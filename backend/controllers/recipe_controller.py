import logging
from mlpro.recommender import recommend_dish

def get_recommendation(input, diet=None, cuisine=None):
    logging.info(f"Controller received: input={input}, diet={diet}, cuisine={cuisine}")
    result = recommend_dish(input, diet, cuisine)
    logging.info(f"Controller returning: {result}")
    return result
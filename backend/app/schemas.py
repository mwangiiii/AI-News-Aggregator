from pydantic import BaseModel
from typing import List

class CategoryUpdate(BaseModel):
    """Schema for updating an article's category"""
    title: str
    category: str

class NewsRequest(BaseModel):
      """Schema for processing a new article with AI models"""
      text: str
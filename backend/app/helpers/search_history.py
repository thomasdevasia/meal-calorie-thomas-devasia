from app.schemas.get_calories import get_calories_response
from app.db.session import SessionLocal
from app.db.models import UserSearchHistory, User

def add_to_search_history(response_data: get_calories_response, user_email: str, search_keyword: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            # print(f"User not found for email: {user_email}")
            return None
            
        # print(f"Logging search history for user {user.id}...")
        search_entry = UserSearchHistory(
            user_id=user.id,
            search_keyword=search_keyword,
            dish_name=response_data.dish_name,
            calories_per_serving=int(response_data.calories_per_serving),
            total_calories=int(response_data.total_calories),
            protein_per_serving=int(response_data.protein_per_serving),
            fat_per_serving=int(response_data.fat_per_serving),
            carbohydrates_per_serving=int(response_data.carbohydrates_per_serving),
            source=response_data.source
        )
        db.add(search_entry)
        db.commit()
        # print("Search history logged successfully")
    except Exception as e:
        db.rollback()
        # print(f"Error logging search history: {e}")
        return None
    finally:
        db.close()
        return True
    

def get_search_history(user_email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            # print(f"User not found for email: {user_email}")
            return None
        
        history = db.query(UserSearchHistory).filter(UserSearchHistory.user_id == user.id).order_by(UserSearchHistory.searched_at.desc()).all()
        return history
    except Exception as e:
        # print(f"Error retrieving search history: {e}")
        return None
    finally:
        db.close()

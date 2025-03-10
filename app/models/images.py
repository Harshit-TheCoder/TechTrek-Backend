from app.models.database import get_db
import gridfs

class Images:

    @staticmethod
    def insert_one(data):
        db = get_db()
        fs = gridfs.GridFS(db)
        with open("example.jpg", "rb") as image_file:
            file_id = fs.put(image_file, filename="example.jpg")

        print("Image stored with ID:", file_id)
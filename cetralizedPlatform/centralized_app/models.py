# from django.db import models
# import numpy as np
# import json

# class FaceData(models.Model):
#     # Field to store names as a list of strings
#     names = models.JSONField()
    
#     # Field to store face encodings as a list of NumPy arrays in their original format
#     face_encodings = models.JSONField()
    
#     def set_face_encodings(self, encodings):
#         """
#         Stores encodings as JSON-serializable lists in the database.
#         """
#         self.face_encodings = [encoding.tolist() for encoding in encodings]
    
#     def get_face_encodings(self):
#         """
#         Retrieves encodings from the database in their original NumPy array format.
#         """
#         return [np.array(encoding) for encoding in self.face_encodings]
    
#     def __str__(self):
#         return f"FaceData with {len(self.names)} names"


from django.db import models
import numpy as np
import face_recognition

class FaceData(models.Model):
    names = models.JSONField(default=list)  # Store names as a JSON list
    face_encodings = models.JSONField(default=list)  # Store encodings as a JSON list

    def set_face_encodings(self, new_encodings):
        """Appends new encodings to the existing encodings list, ensuring uniqueness."""
        current_encodings = self.face_encodings or []

        for encoding in new_encodings:
            # Check if encoding already exists using compare_faces
            is_duplicate = False
            for existing_encoding in current_encodings:
                # Compare encodings, allowing a small threshold for similarity
                results = face_recognition.compare_faces([np.array(existing_encoding)], encoding)
                if any(results):
                    is_duplicate = True
                    break

            # Only append encoding if it's unique
            if not is_duplicate:
                current_encodings.append(encoding.tolist())  # Convert numpy array to list for JSON compatibility

        self.face_encodings = current_encodings

    def set_names(self, new_names):
        """Appends new names to the existing names list, ensuring uniqueness."""
        current_names = self.names or []

        for name in new_names:
            # Only add the name if it doesn't already exist in the list
            if name not in current_names:
                current_names.append(name)

        self.names = current_names

    def get_face_encodings(self):
        """Returns face encodings as numpy arrays."""
        return [np.array(encoding) for encoding in self.face_encodings]

    def get_names(self):
        """Returns all names."""
        return self.names

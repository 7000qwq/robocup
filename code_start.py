class Robocup():
    origin_pics=[]
    item_labelled_pics=[]
    face_item_labelled_pics=[]
    def __init__(self):
        self._detection = None
    def read_pics(self):
        return "Read"
    def detect_items(self):
        return "Detection"
    def detect_faces(self):
        return "Detection"
    def label_faces(self):
        return "Labelled"
    def save_results(self):
        return self._detection




if __name__ == "__main__":
    robocup = Robocup()
    robocup.read_pics()
    robocup.detect_items()
    robocup.detect_faces()
    robocup.label_faces()
    robocup.save_results()

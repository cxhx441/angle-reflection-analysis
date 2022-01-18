from os import rename
import pickle 
import io

class RenameUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        renamed_module = module
        if module in ("Source", "Reflector", "Receiver", "Ray"):
            renamed_module = 'geometric_elements'
        return super(RenameUnpickler, self).find_class(renamed_module, name)

def renamed_load(file_obj):
    return RenameUnpickler(file_obj).load()

def renamed_loads(pickled_bytes):
    file_obj = io.BytesIO(pickled_bytes)
    return renamed_load(file_obj)

def main():
    print("hello?")
    filepath = 'RBHS (real) - T1.pickle'

    with open(filepath, "rb") as input_file:
        print("opend")
        # data = pickle.load(input_file)
        # print(1, data)
        data = renamed_load(input_file)
        print(2, data)
    print("closed")

    with open(filepath[:16]+" - renamed.pickle", "wb") as output_file:
        pickle.dump(data, output_file)
        
if __name__ == "__main__":
    main()

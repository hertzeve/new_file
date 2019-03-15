import os
import time
from code.playIQ import createIndex


if __name__ == "__main__":
    start = time.clock()

    index = createIndex.create_index()
    createIndex.write_index_file(index)
    # create_inverted_index.write_document_map()

    end = time.clock()

    print((end - start))


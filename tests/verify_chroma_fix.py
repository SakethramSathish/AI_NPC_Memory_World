
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.chroma_client import ChromaClient

def test_chroma_embedding_signature():
    print("Testing ChromaClient.get_collection...")
    try:
        # This will trigger the embedding function validation
        collection = ChromaClient.get_collection("test_verification_collection")
        print("Successfully obtained collection!")
        
        # Test adding and querying to ensure the embedding function works
        print("Testing add and query...")
        collection.add(
            documents=["This is a test document"],
            metadatas=[{"source": "test"}],
            ids=["test_id_1"]
        )
        results = collection.query(
            query_texts=["test"],
            n_results=1
        )
        print(f"Query results: {results}")
        
        # Cleanup
        print("Cleaning up...")
        ChromaClient.delete_collection("test_verification_collection")
        print("Verification SUCCESS!")
        
    except Exception as e:
        print(f"Verification FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_chroma_embedding_signature()

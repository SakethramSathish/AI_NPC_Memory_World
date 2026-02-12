
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.chroma_client import ChromaClient

def test_chroma_fix_v3():
    print("Testing ChromaClient.get_collection with name attribute...")
    try:
        # This will trigger the embedding function validation which checks .name()
        collection = ChromaClient.get_collection("test_verification_collection_v3")
        print("Successfully obtained collection!")
        
        # Cleanup
        print("Cleaning up...")
        ChromaClient.delete_collection("test_verification_collection_v3")
        print("Verification SUCCESS!")
        
    except Exception as e:
        print(f"Verification FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_chroma_fix_v3()

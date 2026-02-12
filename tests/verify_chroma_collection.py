
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.chroma_client import ChromaClient

def test_collection_recovery():
    print("Testing Collection get_or_create...")
    collection_name = "test_verification_collection_v2"
    
    try:
        # First call: Should create the collection
        print(f"1. Getting collection '{collection_name}' (First time)...")
        col1 = ChromaClient.get_collection(collection_name)
        print("   Success.")

        # Second call: Should retrieve the SAME collection without error
        print(f"2. Getting collection '{collection_name}' (Second time)...")
        col2 = ChromaClient.get_collection(collection_name)
        print("   Success.")
        
        # Verify it's the same collection object or at least same name
        assert col1.name == col2.name
        print("   Verified collection names match.")

        # Cleanup
        print("Cleaning up...")
        ChromaClient.delete_collection(collection_name)
        print("Verification SUCCESS!")
        
    except Exception as e:
        print(f"Verification FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_collection_recovery()

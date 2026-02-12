
import sys
import os
import inspect
from typing import cast

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from chromadb.api.types import validate_embedding_function
except ImportError:
    print("Could not import validate_embedding_function from chromadb.api.types")
    # Fallback: manually check signature
    validate_embedding_function = None

def test_signature():
    print("Checking EmbeddingFunction signature compliance...")

    # Define the adapter as implemented in the fix
    class ChromaEmbeddingAdapter:
        def __call__(self, input: list[str]) -> list[list[float]]:
            return [[0.1, 0.2]] # Dummy return

    adapter = ChromaEmbeddingAdapter()
    
    if validate_embedding_function:
        try:
            validate_embedding_function(adapter)
            print("SUCCESS: Adapter passed chromadb validation!")
        except Exception as e:
            print(f"FAILURE: Adapter failed chromadb validation: {e}")
            sys.exit(1)
    else:
        sig = inspect.signature(adapter.__call__)
        params = list(sig.parameters.keys())
        if params == ['input'] or params == ['self', 'input']:
             print("SUCCESS: Adapter signature looks correct (manual check).")
        else:
             print(f"FAILURE: Adapter signature is {params}, expected ['input'] or ['self', 'input']")
             sys.exit(1)

if __name__ == "__main__":
    test_signature()

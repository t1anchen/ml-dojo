import datasets
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sentence_transformers.models import StaticEmbedding

datasets.logging.set_verbosity_debug()


def main():
    # Create embeddings for the dataset
    static_embedding = StaticEmbedding.from_model2vec(
        "minishlab/potion-base-8M"
    )
    model = SentenceTransformer(modules=[static_embedding])
    # load dataset
    ds = load_dataset("ai-blueprint/fineweb-bbc-news")

    #
    def create_embeddings(batch):
        embeddings = model.encode(batch["text"], convert_to_numpy=True)
        batch["embeddings"] = embeddings.tolist()
        return batch

    ds = ds.map(create_embeddings, batched=True)


if __name__ == "__main__":
    main()

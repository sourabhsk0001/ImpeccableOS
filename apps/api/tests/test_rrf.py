from src.services.retrieval.rrf import reciprocal_rank_fusion


def test_rrf_scoring_and_ranking():
    # Dense results: doc1 (rank 1), doc2 (rank 2)
    dense = [{"id": "doc1", "content": "dense top"}, {"id": "doc2", "content": "dense second"}]
    # Sparse results: doc2 (rank 1), doc3 (rank 2)
    sparse = [{"id": "doc2", "content": "sparse top"}, {"id": "doc3", "content": "sparse second"}]

    fused = reciprocal_rank_fusion([dense, sparse], k=60, top_n=3)

    # For k=60:
    # doc1: 1/(60+1) = 1/61 = 0.016393
    # doc2: 1/(60+2) + 1/(60+1) = 1/62 + 1/61 = 0.016129 + 0.016393 = 0.032522
    # doc3: 1/(60+2) = 1/62 = 0.016129
    # Expected ranking: doc2 > doc1 > doc3
    assert len(fused) == 3
    assert fused[0]["id"] == "doc2"
    assert fused[1]["id"] == "doc1"
    assert fused[2]["id"] == "doc3"
    assert fused[0]["rrf_score"] > fused[1]["rrf_score"]

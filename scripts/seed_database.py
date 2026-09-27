import asyncio
import os
import sys

# Ensure apps/api is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "api")))

from src.core.database import AsyncSessionLocal, engine, Base
from src.models.dag import SkillNode, PrerequisiteEdge
from src.models.document import DocumentChunk
from src.services.dag.taxonomy import INITIAL_TAXONOMY


async def seed():
    print("Beginning database schema creation and seed procedure...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        # 1. Seed Skills and Prerequisite Edges
        for item in INITIAL_TAXONOMY:
            skill = SkillNode(
                id=item["id"],
                domain=item["domain"],
                name=item["name"],
                description=item["description"],
                depth_level=item["depth_level"],
                mastery_threshold=item["mastery_threshold"]
            )
            await session.merge(skill)
        
        await session.commit()

        for item in INITIAL_TAXONOMY:
            for prereq in item["prerequisites"]:
                edge = PrerequisiteEdge(
                    source_skill_id=prereq,
                    target_skill_id=item["id"],
                    required_mastery=item["mastery_threshold"]
                )
                await session.merge(edge)

        await session.commit()
        print(f"Successfully seeded {len(INITIAL_TAXONOMY)} canonical skill nodes and prerequisite graph.")

        # 2. Seed Reference Corpus Document Chunks
        sample_doc = DocumentChunk(
            id="doc-rag-rrf-k60",
            source_title="Reciprocal Rank Fusion in Production RAG",
            section_title="Formula & Parameter Calibration",
            domain_topic="rag_systems",
            content="Reciprocal Rank Fusion (RRF) with constant k=60 robustly fuses dense cosine embeddings with sparse BM25 text search.",
            authority_level=1,
            is_evolving_topic=False,
            source_url="https://github.com/sourabhsk0007/ImpeccableOS"
        )
        await session.merge(sample_doc)
        await session.commit()
        print("Successfully seeded reference corpus chunks.")


if __name__ == "__main__":
    asyncio.run(seed())

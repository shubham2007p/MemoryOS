from config.prompts import load_specialist_prompt

def test_load_specialist_prompt_fallback():
    """Verify load_specialist_prompt returns correct default strings when fallback happens."""
    learner_prompt = load_specialist_prompt("learner")
    assert "Learning Specialist" in learner_prompt

    non_existent = load_specialist_prompt("ghost")
    assert "specialist reasoning" in non_existent

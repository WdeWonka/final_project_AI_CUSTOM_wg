# BDD Scenarios — CAG Validation Tests

Feature: Context-Augmented Generation (CAG)

  As a system that supports personalised AI responses,
  I want to save and retrieve per-user context
  And use that context to shape the answers returned by /api/ask.

  # -------------------------------------------------------
  # Scenario 1 — maps to test_saves_context_for_user
  # -------------------------------------------------------
  Scenario: Save user context via the API
    Given the server is running
    When I send a POST request to "/api/context" with body:
      """
      {
        "user_id": "ana",
        "key": "audience",
        "value": "explicar como principiante"
      }
      """
    Then the response status code should be 201
    And the response body should be:
      """
      {"saved": true}
      """

  # -------------------------------------------------------
  # Scenario 2 — maps to test_retrieves_context_for_user
  # -------------------------------------------------------
  Scenario: Retrieve stored context for a user
    Given the server is running
    And context has previously been saved for user "ana" with key "audience" and value "explicar como principiante"
    When I send a GET request to "/api/context?user_id=ana"
    Then the response status code should be 200
    And the response body should be a JSON list
    And the list should contain at least one entry with the shape:
      """
      {"key": "<any string>", "value": "<any string>"}
      """

  # -------------------------------------------------------
  # Scenario 3 — maps to test_ask_uses_context_to_influence_later_response
  # -------------------------------------------------------
  Scenario: Context influences the answer returned by /api/ask
    Given the server is running
    And context has been saved for user "ana" with key "audience" and value "explicar como principiante"
    When I send a POST request to "/api/ask" with body:
      """
      {
        "user_id": "ana",
        "question": "¿Qué es la inteligencia artificial?"
      }
      """
    Then the response status code should be 200
    And the response body field "answer" should contain the word "principiante"
    And the response body field "context_used" should contain "audience"

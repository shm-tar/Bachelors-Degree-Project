def test_new_post(new_post):
    assert new_post.title == "Anonymous CV"
    assert new_post.content == "Test Content"
    assert new_post.entity_content == "<p>test</p>"
    assert new_post.user_id == 2

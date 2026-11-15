require "test_helper"

class SessionsControllerTest < ActionDispatch::IntegrationTest
  test "legacy login address redirects to the Devise sign-in form" do
    get "/login"
    assert_redirected_to new_user_session_url
    follow_redirect!
    assert_response :success
  end
end

require "test_helper"

class Admin::DashboardControllerTest < ActionDispatch::IntegrationTest
  include Devise::Test::IntegrationHelpers

  test "administrator can open the dashboard" do
    sign_in users(:one)
    get admin_dashboard_url
    assert_response :success
  end

  test "guest is redirected to sign in" do
    get admin_dashboard_url
    assert_redirected_to new_user_session_url
  end

  test "reader is redirected home" do
    sign_in users(:two)
    get admin_dashboard_url
    assert_redirected_to root_url
  end
end

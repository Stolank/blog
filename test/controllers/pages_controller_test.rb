require "test_helper"

class PagesControllerTest < ActionDispatch::IntegrationTest
  test "should get home" do
    get root_url
    assert_response :success
    assert_select "nav a[href=?]", articles_path
    assert_select "nav a[href=?]", cities_path
  end
end

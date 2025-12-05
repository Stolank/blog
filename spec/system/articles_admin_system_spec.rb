require "rails_helper"

RSpec.describe "Articles admin access", type: :system do
  it "allows admin to open new article page" do
    admin = User.create!(
      name: "Admin",
      email: "admin@example.com",
      password: "password123",
      role: "admin"
    )

    login_as(admin, scope: :user)

    visit "/articles/new"

    expect(page).to have_current_path("/articles/new")
    expect(page).to have_content("Title")
  end

  it "does not allow regular user to open new article page" do
    user = User.create!(
      name: "User",
      email: "user@example.com",
      password: "password123",
      role: "user"
    )

    login_as(user, scope: :user)

    visit "/articles/new"

    expect(page).to have_current_path("/")
    expect(page).to have_content("Недостаточно прав для доступа к этой странице.")
  end

  it "does not allow guest to open new article page" do 
    visit "articles/new"

    expect(page).to have_current_path("/users/sign_in")
  end

  it "allow admin to open edit article page" do 
    admin = User.create!(
      name: "Admin",
      email: "admin@example.com",
      password: "password123",
      role: "admin"
    )
    
    article = Article.create!(
      title: "Test article",
      content: "Some content"
    )

    login_as(admin, scope: :user)
    
    visit "/articles/#{article.id}/edit"

    expect(page).to have_current_path("/articles/#{article.id}/edit")
    expect(page).to have_content("Title")
  end

  it "does not allow  regular user to open edit article page" do 
    user = User.create!(
      name: "User",
      email: "user@example.com",
      password: "password123",
      role: "user"
   )

    article = Article.create!( 
       title: "Test article",
       content: "Some content"

   )

    login_as(user, scope: :user)

    visit "/articles/#{article.id}/edit"
   
    expect(page).to have_current_path("/")
    expect(page).to have_content("Недостаточно прав для доступа к этой странице.")
  end

  it "does not allow guest to open edit article page" do 
    article = Article.create!(
      title: "Test article",
      content: "Some content"
    )

    visit "/articles/#{article.id}/edit"

    expect(page).to have_current_path("/users/sign_in")
  end

  it "allows admin to delete an article" do
    admin = User.create!(
      name: "Admin",
      email: "admin@example.com",
      password: "password123",
      role: "admin"
  )

  article = Article.create(
    title: "Test article",
    content: "Some content"
  )

    login_as(admin, scope: :user)

    visit "/articles/#{article.id}"
 
    click_button "Destroy this article"

    expect(page).to have_current_path("/articles")
    expect(page).to have_no_content("Test article")
  end

  it "does not allow regular user to delete an article" do 
    user = User.create!(
      name: "User",
      email: "user@example.com",
      password: "password123",
      role: "user"
    )

    article = Article.create!(
      title: "Test article",
      content: "Some content"
    )
    
    login_as(user, scope: :user)

    visit "/articles/#{article.id}"    

    expect(page).to have_current_path("/articles/#{article.id}")
    expect(page).to have_no_button("Destroy this article.")     
  end
 
  it "does not allow guest to delete an article" do 
    article = Article.create!(
      title: "Test article",
      content: "Some content"
    )

    visit "/articles/#{article.id}"

    expect(page).to have_current_path("/articles/#{article.id}")
    expect(page).to have_no_button("Destroy this article")
  end
end

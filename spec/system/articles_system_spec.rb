require 'rails_helper'

RSpec.describe "Articles system", type: :system do 
  it "opens the articles index page" do 
    visit "/articles"
    expect(page).to have_content("Articles")
  end

  it "show a single article page" do 
    article = Article.create!(title: "Capybara Test Article", content: "This is a test content")
    
    visit "/articles/#{article.id}"

    expect(page).to have_content("Capybara Test Article")
    expect(page).to have_content("This is a test content")
  end
end


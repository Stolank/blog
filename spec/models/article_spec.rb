require 'rails_helper'


RSpec.describe Article, type: :model do 
  it "is invalid without a title" do
    article = Article.new(content: "Some text")
    expect(article).to be_invalid
  end
  
  it "is valid with a title and content" do 
  article = Article.new(title: "My title", content: "Some text")
  expect(article).to be_valid
  end
end

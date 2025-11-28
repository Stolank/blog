  require 'rails_helper'

  RSpec.describe ArticlesController, type: :controller do

  before do
    allow(controller).to receive(:authenticate_user!).and_return(true)
    allow(controller).to receive(:require_admin).and_return(true)
  end
 
  describe "GET #index" do
    it "returns a succesful response" do 
      get :index
      expect(response).to have_http_status(:ok)
    end
  end

   describe "GET #show" do
     it "returns a successful response" do 
       article = Article.create!(title: "Test Title", content: "Test Content")
       get :show, params: { id: article.id }
       expect(response).to have_http_status(:ok)
     end
   end

   describe "GET #show" do
     it "creates a new article and redirects" do 
       expect {
          post :create, params: { article: { title: "New Title", content: "New Content"} }
       }.to change(Article, :count).by(1)
       
       expect(response).to have_http_status(:see_other).or have_http_status(:found)
     end 
   end

   describe "GET #new" do
    it "returns a successful response" do
      get :new
      expect(response).to have_http_status(:ok)
    end
  end

   describe "PATCH #update" do 
     it "updates the article and redirects" do 
       article = Article.create!(title: "Old Title", content: "Old Content")
       
       patch :update, params: { id: article.id, article: { title: "Update Title" } }

       article.reload
       expect(article.title).to eq("Update Title")

       expect(response).to have_http_status(:see_other).or have_htto_status(:found)
     end
   end
    
    describe "DELETE #destroy" do 
      it "deletes the articles and redirects" do 
        article = Article.create!(title: "To Delete", content: "Delete Me")

        expect {
          delete :destroy, params: { id: article.id } 
        }.to change(Article, :count).by(-1)

        expect(response).to have_http_status(:see_other).or have_http_status(:found)
      end
    end


end

  

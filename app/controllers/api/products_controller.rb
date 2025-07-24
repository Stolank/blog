class Api::ProductsController < ApplicationController
  before_action :authenticate_api_key
  protect_from_forgery with: :null_session
  
  def index
    products = Product.all

    products = products.where("name LIKE ?", "%#{params[:name]}%") if params[:name].present? # Фильтрация по имени 

    products = products.where("price >= ?", params[:min_price]) if params[:min_price].present? # Фильтрация по цене 
    products = products.where("price <= ?", params[:max_price]) if params[:max_price].present?

    products = products.page(params[:page]).per(params[:per_page] || 5) # Пагинация

    render json: products
  end

  def create
    puts "==== CREATE CALLED ===="
    product = Product.new(product_params)
    if product.save
      render json: product, status: :created
    else
      render json: { errors: product.errors.full_messages }, status: :unprocessable_entity
    end
  end

  def destroy
    product = Product.find_by(id: params[:id])
    if product
      product.destroy
      render json: { message: "Product deleted successfully" }, status: :ok
    else
      render json: { error: "Product not found" }, status: :not_found
    end
  end

  def update
  product = Product.find_by(id: params[:id])
  if product
    if product.update(product_params)
      render json: product, status: :ok
    else
      render json: { errors: product.errors.full_messages }, status: :unprocessable_entity
    end
  else
    render json: { error: "Product not found" }, status: :not_found
  end
end

  private

  def product_params
    params.require(:product).permit(:name, :price)
  end
end
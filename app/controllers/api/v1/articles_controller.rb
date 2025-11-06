module Api
  module V1
    class ArticlesController < Api::BaseController
      def index

        scope = Article.all 

        # Поиск ?q=ruby
            if params[:q].present?
          q = "%#{params[:q]}%"
          scope = scope.where("title LIKE ? COLLATE NOCASE", q)
        end

        scope = scope.order(created_at: :desc)

        # Paginate
        result = paginate_scope(scope) 

        render json: {
          data: result[:items].as_json(only: %i[id title body created_at]),
          meta: result[:meta]
        }
      end

      def show
        article = Article.find(params[:id])

        render json: {
          data: articles.as_json(only: %i[id title body created_at])
        }
      end
    end
  end
end
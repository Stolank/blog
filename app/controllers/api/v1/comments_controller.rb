module Api
  module V1
    class CommentsController < Api::BaseController
      def index 
        roots = Comment.where(parent_id: nil).order(created_at: :asc)

        render json: {
          data: roots.map { |c| comment_tree(c) }
        }
      end

      private

      def comment_tree(comment)
        {
          id: comment.id,
          body: comment.body,
          children: comment.children.order(created_at: :asc).map { |child| comment_tree(child) }
        }
      end
    end
  end
end
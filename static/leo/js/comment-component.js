let comment_component = Vue.component('comment-component', {
    data: function () {
        return {
            confirm_delete_comment: false,

            profile_id: profile_id
            // current_profile_id: JSON.parse("{% if profile %}{{profile.id}}{%else%}0{%endif%}")
        }
    },
    methods: {
        ShowConfirmDeleteComment: function () {

            this.confirm_delete_comment = true
        },
        ConfirmDeleteComment: function (comment_id) {


            this.confirm_delete_comment = false
            let url = delete_comment_url
            let posting = $.post(url, {
                comment_id: comment_id,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            })

            posting.done(function (data) {

                if (data.done) {
                    delete_comment(comment_id)
                }

            })


        },
        CancelDeleteComment: function () {
            this.confirm_delete_comment = false
        },
    },
    props: ['comment'],
    template:comment_template,
})







// must be initialized
// let comments = JSON.parse(`{{comments_s|escapejs}}`)
// let my_like = JSON.parse("{% if my_like %}true{% else %}false{% endif %}")
// let page_id = JSON.parse("{{page.id}}")
// let likes_count = JSON.parse("{{page.likes.all|length}}")
// let object_id=JSON.parse("{{page.id}}")
// let add_comment_url="{% url 'app:add_comment' %}"
// let delete_comment_url="{% url 'app:delete_comment' %}"    
// let profile_id=JSON.parse("{% if profile %}{{profile.id}}{% else %}0{% endif %}")

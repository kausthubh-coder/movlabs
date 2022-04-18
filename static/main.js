var app = new Vue({
    el: '#app',
    data: {
        message: 'Search for movie'
    },
    methods:{
        search: function(){
            let url = this.message.replace(/\s/g, '-')
            window.location.replace("/search/"+url);
        }
    }
  })
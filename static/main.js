var app = new Vue({
    el: '#app',
    data: {
        message: ''
    },
    methods:{
        search: function(){
            let url = this.message.replace(/\s/g, '-');
            window.location.replace("/search/"+url);
        },
        home: function(){
            window.location.href = "http://www.movlabs.herokuapp.com";
        }
    }
  })
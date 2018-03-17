var vm = new Vue ({
	el: '#form',
	data: {
        massege: 'Ты Хуй',
        pass2: 0,
        pass1:0
    },
    methods: {
        different_pass(){
            if(this.pass1===this.pass2)
            {
                this.messege="ты облажался"
            }
        }
    }
});
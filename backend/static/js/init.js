function init() {
    return {
        menu: "",
        loading: true,
        forWeek: "",

        async loadList() {
            console.log('Loading List');
            this.loading = true;
            this.menu= "";
            this.menu = await (await fetch(`/api/menu?d=${encodeURIComponent(this.forWeek)}`)).json();
            console.log(this.menu);
            this.loading = false;
        },

        async adjustDate(dir) {
            // add a week to current forWeek
            const parts = this.forWeek.split('/');
            const date = new Date(parts[2], parts[0] - 1, parts[1]);
            if (dir === 'back') {
                date.setDate(date.getDate() - 7);
            } else {
                date.setDate(date.getDate() + 7);
            }
            const mm = String(date.getMonth() + 1).padStart(2, '0');
            const dd = String(date.getDate()).padStart(2, '0');
            const yyyy = date.getFullYear();
            this.forWeek = `${mm}/${dd}/${yyyy}`;
            await this.loadList();
        },

        async loadToday() {
            // Calculate the date of the Monday of this week in MM/DD/YYYY format
            const today = new Date();
            const monday = new Date(today);
            monday.setDate(today.getDate() - ((today.getDay() + 6) % 7));
            const mm = String(monday.getMonth() + 1).padStart(2, '0');
            const dd = String(monday.getDate()).padStart(2, '0');
            const yyyy = monday.getFullYear();
            const mondayStr = `${mm}/${dd}/${yyyy}`;
            this.forWeek = mondayStr;
            await this.loadList();
        },

        delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms))
        },
          


    }
}
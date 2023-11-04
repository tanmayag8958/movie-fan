<template>
    <div v-if="Object.keys(chartObject).length" class="card card-container">
        <div class="card-body">
            <Line :data="chartObject['data']" :options="chartObject['options']"/>
        </div>
    </div>
</template>

<script>
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'
import {Line} from 'vue-chartjs'
import axios from "axios";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

export default {
    name: 'LineChart',
    components: {
        Line
    },
    props: {
        tile: {
            type: Object
        },
        selectedFilters: {
            type: Object
        }
    },
    watch: {
        selectedFilters: {
            handler(newValue, oldValue) {
                console.log(JSON.parse(JSON.stringify(newValue)), JSON.parse(JSON.stringify(oldValue)));
                let valueChanged = false;
                Object.keys(oldValue).forEach(tile_key => {
                    if (oldValue[tile_key] !== newValue[tile_key]) {
                        valueChanged = true;
                    }
                });
                console.log('valueChanged :- ', valueChanged);
                if (valueChanged) {
                    this.fetchTile();
                }
            },
            deep: true
        }
    },
    data() {
        return {
            chartObject: {}
        }
    },
    mounted: function () {
        this.setup();
    },
    methods: {
        setup: function () {
            this.chartObject = this.tile['tile']['result'];
        },
        fetchTile: function () {
            let filterDictString = '{';
            Object.keys(this.selectedFilters).forEach((filterName, index) => {
                filterDictString += `"${filterName}": "${this.selectedFilters[filterName] === 'Select' ? '' : this.selectedFilters[filterName]}"`
                if (index !== Object.keys(this.selectedFilters).length - 1) filterDictString += ','
            });
            filterDictString += '}'
            console.log('filterDictString :- ', filterDictString);
            axios({
                method: 'get',
                url: 'http://localhost:8000/dashboard/tiles/' + `?filters=${filterDictString}&tile_key=${this.tile['tile_key']}`,
            }).then(response => {
                this.chartObject = response.data['tile']['result'];
            });
        }
    }
}
</script>
<style>
.card-container {
    background-color: #2B2B2B;
    border: none;
}
</style>
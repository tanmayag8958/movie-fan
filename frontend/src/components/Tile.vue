<template>
    <div class="card card-container">
        <template v-if="tile['type'] === 'chart'">
            <line-chart
                    :tile-result="tileResult"
            />
        </template>
        <template v-else-if="tile['type'] === 'count'">
            <count-tile
                    :tile-result="tileResult"
            />
        </template>
    </div>
</template>

<script>
import axios from "axios";
import CountTile from "@/components/CountTile.vue";
import LineChart from "@/components/LineChart.vue";


export default {
    name: 'TileViewer',
    components: {
        LineChart,
        CountTile,
    },
    props: {
        tile: {
            type: Object
        },
        selectedFilters: {
            type: Object
        },
        selectedMedia: {
            type: Object
        }
    },
    watch: {
        selectedFilters: {
            handler(newValue, oldValue) {
                let valueChanged = false;
                Object.keys(oldValue).forEach(tile_key => {
                    if (oldValue[tile_key] !== newValue[tile_key]) {
                        valueChanged = true;
                    }
                });
                if (valueChanged) {
                    this.fetchTile();
                }
            },
            deep: true
        }
    },
    data() {
        return {
            tileResult: {}
        }
    },
    beforeMount: function () {
        this.emitter.on('media-changes', this.fetchTile);
    },
    beforeUnmount: function () {
        this.emitter.off('media-changes', this.fetchTile);
    },
    mounted: function () {
        this.setup();
    },
    methods: {
        setup: function () {
            this.tileResult = this.tile['tile']['result'];
        },
        fetchTile: function () {
            let filterDictString = '{';
            Object.keys(this.selectedFilters).forEach((filterName, index) => {
                filterDictString += `"${filterName}": "${this.selectedFilters[filterName] === 'Select' ? '' : this.selectedFilters[filterName]}"`
                if (index !== Object.keys(this.selectedFilters).length - 1) filterDictString += ','
            });
            filterDictString += '}'
            axios({
                method: 'get',
                url: 'http://localhost:8000/dashboard/tiles/' + `?filters=${filterDictString}&tile_key=${this.tile['tile_key']}&media=${this.selectedMedia['name']}`,
            }).then(response => {
                if (!Object.keys(response.data).length) this.tileResult = {};
                else this.tileResult = response.data['tile']['result'];
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
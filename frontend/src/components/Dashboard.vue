<template>
    <div class="card m-0 p-0 filter-header">
        <h2 class="header-name p-3">MOVIE FAN</h2>
    </div>
    <div class="container dashboard-container" style="max-width: 95% !important;">
        <div class="row">
            <div class="col-6">
                <div class="card card-container">
                    <div class="card-body">
                        <div class="movie-count-container p-2">
                            <span class="movie-label">Total Number of Movies </span>
                            <span class="movie-label">Name of director </span>
                        </div>
                    </div>
                </div>
            </div>
            <div
                    v-for="_filter in filters"
                    :key="_filter['name']"
                    class="col-3"
            >
                <div class="card card-container">
                    <div class="card-body p-0">
                        <div class="row display-flex justify-content-center align-items-center m-auto">
                            <div class="col-10 p-4 filter-container">
                                <span class="filter-label">{{ _filter['label'] }}: </span>
                                <span class="filter-label"> {{ selectedFilters[_filter['name']] }} </span>
                            </div>
                            <div class="col-2 float-right p-0">
                                <div class="dropdown" style="cursor:pointer;">
                                    <div class="dropdown-toggle filter-dropdown" id="dropdownMenuButton"
                                         data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    </div>
                                    <div class="dropdown-menu dropdown-menu-right dropdown-menu-container"
                                         aria-labelledby="dropdownMenuButton">
                                        <a
                                                v-for="value in _filter['values']"
                                                :key="_filter['name'] + '-' + value"
                                                class="dropdown-item"
                                                @click="handleFilterSelection(_filter['name'], value)"
                                        >
                                            {{ value }}
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <template v-if="chartTiles.length">
            <div class="row pt-5">
                <div
                        v-for="chartTile in chartTiles"
                        :key="chartTile['tile_key']"
                        class="col-6"
                >
                    <line-chart
                            :tile="chartTile"
                            :selected-filters="selectedFilters"
                    />
                </div>
            </div>
        </template>
    </div>
</template>

<script>
import axios from "axios";
import LineChart from "@/components/LineChart.vue";

export default {
    name: 'DashboardViewer',
    components: {
        LineChart
    },
    data() {
        return {
            filters: [],
            selectedFilters: {},
            tiles: [],
            chartTiles: [],
            countTiles: []
        }
    },
    mounted: function () {
        this.fetchFilters();
        this.fetchTiles();
    },
    methods: {
        deepCopy: function (value) {
            return JSON.parse(JSON.stringify(value))
        },
        handleFilterSelection: function (filterName, valueSelected) {
            let currentFilters = this.deepCopy(this.selectedFilters);
            currentFilters[filterName] = valueSelected;
            this.selectedFilters = Object.assign({}, currentFilters);
        },
        fetchTiles: function () {
            axios({
                method: 'get',
                url: 'http://localhost:8000/dashboard/tiles/',
            }).then(response => {
                this.tiles = response.data;
                this.tiles.forEach(tile => {
                    if (tile['type'] === 'chart') {
                        this.chartTiles.push(tile);
                    } else if (tile['type'] === 'count') {
                        this.countTiles.push(tile);
                    }
                });
            });
        },

        fetchFilters: function () {
            axios({
                method: 'get',
                url: 'http://localhost:8000/data/filters/',
            }).then(response => {
                const response_data = response.data;
                response_data.forEach(_filter => {
                    this.selectedFilters[_filter['name']] = 'Select';
                });
                this.filters = response_data;
                this.filters.forEach(_filter => {
                    _filter['values'] = ['Select'].concat(_filter['values'])
                });
            });
        }
    }
}
</script>
<style>
.dashboard-container {
    margin-top: 4%;
}

.card-container {
    background-color: #2B2B2B;
    border: none;
}

.filter-header {
    background-color: #2B2B2B;
    border: none;
}

.header-name {
    margin: 0 0 0 2.5%;
    font-weight: 600;
    background-image: linear-gradient(to left, #ffffff, #ffffff);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-align: start;
}

.filter-label {
    margin: 0 0 0 2.5%;
    font-weight: 600;
    background-image: linear-gradient(to left, #ffffff, #ffffff);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-align: start;
}

.filter-dropdown {
    color: white;
    font-size: 20px;
}

.filter-container {
    border-right: 1px solid #3e3e3e;
}

.movie-count-container {

}

.movie-label {
    margin: 0 0 0 2.5%;
    font-weight: 600;
    background-image: linear-gradient(to left, #ffffff, #ffffff);
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    text-align: start;
}

.dropdown-menu-container {
    overflow-y: auto;
    position: absolute !important;
    height: 500px;
    scroll-behavior: smooth;
    background-color: #2B2B2B;
}
</style>
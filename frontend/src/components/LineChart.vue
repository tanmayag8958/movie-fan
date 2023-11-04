<template>
    <div v-if="Object.keys(tileResult).length" class="card card-container">
        <div class="card-body">
            <Line :data="tileResult['data']" :options="tileResult['options']"/>
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
    Legend, Colors
} from 'chart.js'
import {Line} from 'vue-chartjs'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Colors
)

export default {
    name: 'LineChart',
    components: {
        Line
    },
    props: {
        tileResult: {
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
    }
}
</script>
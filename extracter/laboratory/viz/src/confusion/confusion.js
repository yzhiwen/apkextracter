class ConfusionBar {
    constructor() {
        this.init();
    }

    init() {
        let margin = { top: 30, right: 30, bottom: 70, left: 60 };
        let width = 860 - margin.left - margin.right;
        let height = 600 - margin.top - margin.bottom;
        this.margin = margin;
        this.width = width;
        this.height = height;

        this.svg = d3.select("#my_dataviz")
            .style("display", "flex")
            .style("flex-direction", "column")
            .style("justify-content", "center")
            .style("align-items", "center")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        this.x = d3.scaleBand()
            .range([0, width])
            .padding(0.2);
        this.xAxis = this.svg.append("g")
            .attr("transform", "translate(0," + height + ")")

        this.y = d3.scaleLinear()
            .range([height, 0]);
        this.yAxis = this.svg.append("g")
            .attr("class", "myYaxis")
    }

    setBarClickCallback(callback) {
        this.onBarClickCallback = callback;
    }

    build(data) {
        let that = this;
        let x = this.x;
        let y = this.y;
        let width = this.width;
        let height = this.height;
        let margin = this.margin;

        this.x.domain(data.map(function(d) { return d.name; }))
        this.xAxis.call(d3.axisBottom(this.x))

        this.y.domain([0, d3.max(data, function(d) { return d.value })]);
        this.yAxis.transition().duration(1000).call(d3.axisLeft(this.y));

        var u = this.svg.selectAll("rect")
            .data(data)

        u
            .enter()
            .append("rect")
            .merge(u)
            .transition()
            .duration(1000)
            .attr("x", function(d) { return x(d.name); })
            .attr("y", function(d) { return y(d.value); })
            .attr("width", this.x.bandwidth())
            .attr("height", function(d) { return height - y(d.value); })
            .attr("fill", "#69b3a2")

        u
            .exit()
            .remove()

        this.svg.selectAll("rect")
            .on("click", function(event, data) {
                if (!that.onBarClickCallback) return;
                else that.onBarClickCallback(data);
            })
    }
}

export default ConfusionBar;
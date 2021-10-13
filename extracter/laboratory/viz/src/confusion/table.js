import "./table.css"

class ConfusionTable {
    constructor() {}

    leafs(root, list) {
        if (!list || !root) return;
        if (!root.hasChildren()) {
            list.push(root);
            return;
        }

        for (const child of root.getChildrenList()) {
            this.leafs(child, list);
        }
    }

    build(root) {
        let list = root.getChildrenList();
        this.buildContent(list);
    }

    bulidHeader(titles) {
        this.titles = titles;
    }

    buildContent(list) {
        d3.select("#my_dataviz").selectAll("table").remove();
        let table = d3.select("#my_dataviz")
            .append("table");

        // let titles = this.titles;
        // let headers = table.append('thead').append('tr')
        //     .selectAll('th')
        //     .data(titles).enter()
        //     .append('th')
        //     .text(d => d);

        let rows = table.append('tbody').selectAll('tr')
            .data(list).enter()
            .append('tr');

        let keys = ["clazz", "fRawPrivateCount", "mRawPrivateCount"]

        rows.selectAll('td')
            .data(d => keys.map(function(key) {
                return { value: d[key] }
            }))
            .enter()
            .append('td')
            .text(d => d.value)
    }
}

export default ConfusionTable;
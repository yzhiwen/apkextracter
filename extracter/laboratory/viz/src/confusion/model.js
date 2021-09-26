export default class Node {
    constructor(name) {
        this.name = name;
        this.parent = null;
        this.children = new Array();
        this.childrenMap = new Map(); // <string, Node>
        this.value = 0;
    }

    build(item) {
        if (!item || !item.clazz) return;

        let clazz = item.clazz;
        let index = clazz.indexOf("/");

        let first = index === -1 ? clazz : clazz.substring(0, index);
        if (!this.childrenMap.has(first)) {
            let child = new Node(first);
            this.childrenMap.set(first, child);
            this.children.push(child);
        }
        let child = this.childrenMap.get(first);

        if (index === -1) {
            child.value = item.fRawPrivateCount + item.mRawPrivateCount;
        } else {
            let substring = clazz.substring(index + 1);
            item.clazz = substring;
            child.build(item);
        }
        child.parent = this;
        this.value += item.fRawPrivateCount + item.mRawPrivateCount;
    }

    toJson() {
        let children = [];
        for (const child of this.childrenMap.values()) {
            children.push(child.toJson());
        }
        return {
            name: this.name,
            children: children,
            value: this.value,
            parent: this.parent
        }
    }
}
export default class Node {
    constructor(parent, name) {
        this.name = name;
        this.clazz = (parent && parent.clazz ? parent.clazz + "/" : "") + (name ? name : "");
        this.parent = parent;
        this.childrenMap = new Map(); // <string, Node>
        this.init();
    }

    init() {
        this.fRawPrivateCount = 0;
        this.fPrivateCount = 0;
        this.fCount = 0;
        this.mRawPrivateCount = 0;
        this.mPrivateCount = 0;
        this.mCount = 0;
        this.value = 0;
    }

    plus(item) {
        this.fRawPrivateCount += item.fRawPrivateCount;
        this.fPrivateCount += item.fCount;
        this.fCount += item.fCount;
        this.mRawPrivateCount += item.mRawPrivateCount;
        this.mPrivateCount += item.mPrivateCount;
        this.mCount += item.mCount;
        this.value += item.fRawPrivateCount + item.mRawPrivateCount;
    }

    build(item) {
        if (!item || !item.clazz) return;

        let clazz = item.clazz;
        let index = clazz.indexOf("/");

        let first = index === -1 ? clazz : clazz.substring(0, index);
        if (!this.childrenMap.has(first)) {
            let child = new Node(this, first);
            this.childrenMap.set(first, child);
        }
        let child = this.childrenMap.get(first);

        if (index != -1) {
            let substring = clazz.substring(index + 1);
            item.clazz = substring;
            child.build(item);
        } else {
            child.plus(item);
        }
        this.plus(item);
    }

    hasChildren() {
        return this.childrenMap.size > 0;
    }

    getChildrenList() {
        let list = Array.from(this.childrenMap.values());
        return list.sort((a, b) => b.value - a.value);
    }
}
import { Product } from "./Product";

export class Category {
    categoryName: string = "";
    categoryImage: string = "";
    products: Product[] = [];

    constructor(categoryName = "", products = []) {
        this.categoryName = categoryName;
        this.products = products;
    }
}
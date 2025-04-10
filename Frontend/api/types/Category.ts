import { Product } from "./Product";

export class BasicCategory {
    categoryId: number = 0;
    categoryName: string = "";
    categoryImage: string = "";

    constructor(categoryId = 0, categoryName = "", categoryImage = "") {
        this.categoryId = categoryId;
        this.categoryName = categoryName;
        this.categoryImage = categoryImage;
    }
}

export class Category extends BasicCategory {
    categoryId: number = 0;
    categoryName: string = "";
    categoryImage: string = "";
    products: Product[] = [];

    constructor(categoryId = 0, categoryName = "", categoryImage = "", products = []) {
        super(categoryId, categoryName, categoryImage);
        this.products = products;
    }
}
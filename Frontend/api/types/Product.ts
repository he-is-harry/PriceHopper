export class Product {
    productId: number = 0;
    name: string = "";
    price: number = 0;
    sciPrice: string | null = null;
    company: string = "";
    url: string = "";
    image: string | null = null;

    constructor(productId = 0, name = "", price = 0, sciPrice = null, company = "", url = "", image = null) {
        this.productId = productId;
        this.name = name;
        this.price = price;
        this.sciPrice = sciPrice;
        this.company = company;
        this.url = url;
        this.image = image;
    }
}
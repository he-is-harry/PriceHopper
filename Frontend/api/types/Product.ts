export class Product {
    name: string;
    price: number;
    sciPrice: string | null;
    company: string;
    url: string;
    image: string | null;

    constructor(name = "", price = 0, sciPrice = null, company = "", url = "", image = null) {
        this.name = name;
        this.price = price;
        this.sciPrice = sciPrice;
        this.company = company;
        this.url = url;
        this.image = image;
    }
}
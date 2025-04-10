package ca.harryhe.pricehopper.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import ca.harryhe.pricehopper.dto.BasicCategoryResult;
import ca.harryhe.pricehopper.dto.CategoryResult;
import ca.harryhe.pricehopper.dto.ProductResult;
import ca.harryhe.pricehopper.service.SearchService;

@RestController
@RequestMapping(path = "rest/search")
public class SearchController {
	
	private final SearchService searchService;
	
	public SearchController (SearchService searchService) {
		this.searchService = searchService;
	}
	
	// Retrieves the categories and subsequent products to display on the home page
	@GetMapping(path = "/homepage")
	public List<CategoryResult> getHomeData() {
		return searchService.getHomeData();
	}
	
	// Retrieves the categories to display as recommended
	@GetMapping(path = "/recommended")
	public List<CategoryResult> getRecommendedCategories() {
		return searchService.getRecommendedCategories();
	}
	
	// Searches the categories based on a text prompt
	@GetMapping(path = "/categories")
	public List<BasicCategoryResult> getRelevantCategories(@RequestParam(required = true) String search) {
		return searchService.getRelevantCategories(search);
	}
	
	// Searches the products based on a text prompt or category
	// Returns ReponseEntity<List<ProductResult>> or ReponseEntity<String>
	@GetMapping(path = "/products")
	public ResponseEntity<?> searchProducts(
			@RequestParam(required = false) String search,
			@RequestParam(required = false) Integer categoryId,
			@RequestParam(required = false) Integer limit) {
		// Input is validated where only one field is specified
		if ((search == null || search.isBlank()) && categoryId == null) {
			// Both blank
			return ResponseEntity
					.status(HttpStatus.BAD_REQUEST)
					.body("Search and category cannot both be undeclared");
		} else if (search != null && !search.isBlank() && categoryId != null) {
			// Both declared
			return ResponseEntity
					.status(HttpStatus.BAD_REQUEST)
					.body("Search and category cannot both be declared");
		}
		
		// The default value for the limit is 10
		if (limit == null) limit = 10;
		
		List<ProductResult> searchResult = searchService.search(search, categoryId, limit);
		
		return ResponseEntity.status(HttpStatus.OK).body(searchResult);
	}
}

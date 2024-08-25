package ca.harryhe.pricehopper.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import ca.harryhe.pricehopper.model.view.CategoryResult;
import ca.harryhe.pricehopper.service.SearchService;

@RestController
@RequestMapping(path = "rest/search/")
public class SearchController {
	
	private final SearchService searchService;
	
	public SearchController (SearchService searchService) {
		this.searchService = searchService;
	}
	
	// Retrieves the categories and subsequent products to display on the home page
	@GetMapping(path = "homepage")
	public List<CategoryResult> getHomeData() {
		return searchService.getHomeData();
	}
	
	// Retrieves the categories to display as recommended
	@GetMapping(path = "recommended")
	public List<CategoryResult> getRecommendedCategories() {
		return searchService.getRecommendedCategories();
	}
}

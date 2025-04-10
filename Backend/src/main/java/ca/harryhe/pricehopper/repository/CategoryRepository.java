package ca.harryhe.pricehopper.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import ca.harryhe.pricehopper.model.Category;

@Repository
public interface CategoryRepository extends JpaRepository<Category, Long> {
	@Query("SELECT c FROM Category c WHERE c.categoryId=:categoryId")
	Category findCategoryById(@Param("categoryId") long categoryId);
	
	@Query("SELECT c FROM Category c WHERE lower(c.categoryName) LIKE :query")
	List<Category> searchCategoriesByName(@Param("query") String query);
	
}

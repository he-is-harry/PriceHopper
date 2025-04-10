package ca.harryhe.pricehopper.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import ca.harryhe.pricehopper.dto.ProductSearchDTO;
import ca.harryhe.pricehopper.model.Product;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
	// Searches should take the form of full text identifiers, here we often use the form
	// word | word | word
	// Use the named native query in Product entity
	@Query(nativeQuery = true, name = "searchProductsByName")
	List<ProductSearchDTO> searchProductsByName(@Param("parsedSearch") String parsedSearch, @Param("limit") Integer limit);
	
}

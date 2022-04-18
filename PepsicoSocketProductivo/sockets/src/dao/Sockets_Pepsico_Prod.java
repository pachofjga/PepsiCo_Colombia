package dao;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import javax.net.ServerSocketFactory;

public class Sockets_Pepsico_Prod {
  private static final int PORT_NUM = 15009;
  private static final String DB_DRIVER = "oracle.jdbc.driver.OracleDriver";
  private static final String DB_CONNECTION ="jdbc:oracle:thin:@192.168.1.45:1521:VOCOLLECT";
  private static final String DB_USER = "VLINK";
  private static final String DB_PASSWORD = "talkman";
  
   
  public static void main(String args[]) throws SQLException, ClassNotFoundException {
    
	  
	  try{
          try {
			updateRecordIntoDbUserTable();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
          }catch(SQLException e) {
  			System.out.println(e.getMessage());
  		  } 

  }
  
/** update registro
 * @throws IOException */
  
  private static void updateRecordIntoDbUserTable() throws SQLException, IOException {
	  	Connection dbConnection = null;
		Statement statement = null;

		ServerSocketFactory serverSocketFactory = ServerSocketFactory.getDefault();		
		ServerSocket serverSocket = null;
		try {
		      serverSocket = serverSocketFactory.createServerSocket(PORT_NUM);
		    }catch (IOException ignored) {
		      System.err.println("Unable to create server");
		      System.exit(-1);
		    }
		System.out.println("Listening Server running on port:"+ PORT_NUM);
		
		while (true) {
		      Socket socket = null;
		      try {
		        socket = serverSocket.accept();
		        InputStream is = socket.getInputStream();
		        BufferedReader br = new BufferedReader(new InputStreamReader(is, "US-ASCII"));
		        
		        String line = null;
		        
		        while ((line = br.readLine()) != null) {
		          System.out.println(line);		
				  				  
				  try {
						dbConnection = getDBConnection();
						statement = dbConnection.createStatement();

						//System.out.println(updateTableSQL);
						//System.out.println(line);

						// execute update SQL statement
						//statement.execute(updateTableSQL);
						statement.execute(line);

						System.out.println("Record is updated to Sel_assigments table!");

					} catch (SQLException e) {

						System.out.println(e.getMessage());

					} finally {

						if (statement != null) {
							br.close();
							statement.close();
						}

						if (dbConnection != null) {
							dbConnection.close();
						}

					}
				  
		        }
		      }
		        catch (IOException exception) {
		            // Just handle next request.
		          } finally {
		            if (socket != null) {
		              try {        	  
		                  socket.close();
		                  //serverSocket.close();
		                  System.out.println("Conexion Cerrada!");
		              } catch (IOException ignored) {
		              }
		            }
		          }
		      }
  		          
		/**String updateTableSQL = "UPDATE sel_assignments"
				+ " SET goaltime = '10' "
				+ " WHERE assignmentId = '54188'";
				*/

		

	}
  
/** Conexión BD*/  
  private static Connection getDBConnection(){

		Connection dbConnection = null;

		try {

			Class.forName(DB_DRIVER);

		} catch (ClassNotFoundException e) {

			System.out.println(e.getMessage());

		}

		try {
			
			dbConnection = DriverManager.getConnection(DB_CONNECTION, DB_USER,DB_PASSWORD);
			System.out.println("Conexion exitosa!");
			return dbConnection;

		} catch (SQLException e) {

			System.out.println(e.getMessage());

		}

		return dbConnection;

	}
  
}